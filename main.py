import sys
import json
import gflags

FLAGS = gflags.FLAGS

def main():
    # Step 1: Get data.
    with open(FLAGS.input) as f:
        data = json.load(f)

    for person in data:
        img = person["img"]
        img_html = "<img src='{}'>".format(img)
        name = person["name"].encode('utf-8')

        # Make 2 cards per person.
        create_anki_card(FLAGS.collection_path, FLAGS.deck_name, name, img_html)
        create_anki_card(FLAGS.collection_path, FLAGS.deck_name, img_html, name)

def create_anki_card(coll_file, deck_name, card_front, card_back):
    ''' based on addToAnki
    '''
    import sys, re, unicode_support_checker
    from anki import Collection as aopen

    # todo Not even this works. It refuses to embed the newlines in the Card
    card_back = re.sub(r"\\n", "\n", card_back)

    # All Decks are in a single Collection
    print("Get Collection/Deck '"+coll_file+"/"+deck_name+"'")
    deck = aopen( coll_file );
    deckId = deck.decks.id( deck_name )

    # todo Not sure why a simple 'select' doesnt do the model stuff for me...
    deck.decks.select( deckId )
    basic_model = deck.models.byName('Basic')
    basic_model['did'] = deckId
    deck.models.save( basic_model )
    deck.models.setCurrent( basic_model )

    # todo I don't see any other ways to prevent creating a new Deck
    # if deck.cardCount == 0:
    #     sys.exit("ERROR: Collection/Deck '"+coll_file+"/"+deck_name+"' does not exist.")

    print("Deck has "+str(deck.cardCount())+" cards")

    # Build the card
    # todo Using .decode('utf-8'), I no longer get 'duplicate card' errors :p
    print("Make a new Card for: "+card_front)
    fact            = deck.newNote()
    fact['Front']   = card_front.decode('utf-8')
    fact['Back']    = card_back.decode('utf-8')

    # Add Card to the Deck
    try:
        deck.addNote( fact )
    except:
        e = sys.exc_info()[0]
        if hasattr(e, "data"):
            sys.exit("ERROR: Could not add '"+e.data['field']+"': "+e.data['type'])
        else:
            sys.exit(e)

    # Done.
    print("Save the Deck")
    deck.save()
    deck.close()


if __name__ == '__main__':
    gflags.DEFINE_string("input", "example.json", "JSON file with input data for index cards.")
    gflags.DEFINE_string("deck_name", "example", "Name of deck.")
    gflags.DEFINE_string("collection_path", "/Users/Andrew/Documents/Anki/rc/collection.anki2", "Path to Anki collection file.")

    FLAGS(sys.argv)

    main()
