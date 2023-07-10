The S.O.F.T. (by Python Mode command)

This is the Sophisticated Organizer For Thoughtful people

It consists of three components:
        Arrange Dir  - if you have some directory with a bunch of unsorted files this tool is for you.
                       It helps to tidy up the specified directory and normalize some names.

        Notebook     - as its name says it's a container for your notes which is very useful if you
                       like using CLI while working or doing your usual stuff.
                       You can create notes, tag them, search through the collection delete and overwrite

        Contact book - Every person has friends and acquaintances. And you are not the exception!
                       Add contacts by giving there names, specifying phone number, email, birthday and
                       ZIP address. Don't forget about the birthday of your friend using command
                       "search bthd"

All the components can be called from the Main Menu which you can see right after The S.O.F.T. starts

Arrange Dir:
        If you choose this component it will ask you for a path to a directory which
        you want to arrange.
        The files in the directory will be grouped by type, names will be normalized by
        stripping umbigious characters and transliterated if letters are not in ASCII range.
        Empty directories will be removed.
        The tool recognizes images, documents, unpacks archives etc

Notebook available commands:
        
        add note     - Adds a note. You will be prompted for title and content.
        add tag      - Adds a tag for the note. You should specify note ID.
        clear tags   - Clears all tags for a note with a specified ID.
        del note     - Deletes a note by id.
        del tag      - Deletes a tag by tag's value.
        exit         - Quits the program.
        find note    - Finds notes by a keyword or a tag.
        hello        - Shows greeting.
        help         - Shows this help.
        overwrite    - Overwrites a note with some ID setting new title and content.
        search id    - Prints Note with a specified ID.
        search tag   - Outputs notes associated with a specific tag.
        show all     - Shows all notes, divided by pages. You can set number of items per page.
        show tags    - Shows the list of all tags.
        sort by tags - Outputs all notes sorted by tags.
        untag        - Removes a specific tag from a specific note.

Contact book available commands:
        add             - Adds a contact. Specify name, phone, birthday and optionally email and address
        change birthday - usage: change birthday name new_birthday.
        change name     - usage: change name old_name new_name.
        change phone    - usage: change phone name old_number new_number.
        delete          - Deletes a contact by the name.
        exit            - quits the program.
        find            - looks through contacts names and phones by a key.
        hello           - Shows a greeting.
        help            - Shows this help.
        new phone       - usage: new phone name phone_number.
        remove phone    - usage: remove phone name phone_number.
        search bthd     - Search in the address book who has a birthday in the coming days.
        show all        - prints all contacts with pagination.
