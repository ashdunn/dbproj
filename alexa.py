import mysql.connector as mysql
import speech_recognition as sr
from tkinter import *
from tkinter import ttk
import time


def recognize_speech_from_mic(recognizer, microphone):

    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
        response["transcription"] = response["transcription"].replace("equals", "=")
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


# determines if the input is a valid query phrase
def validator(query):
    spaceless = query.lower().split()
    if spaceless[0] != "select":
        return False

    if "from" not in query:
        return False

    return True


# converts valid query phrase into a valid query
# automatically done: select star -> select *, percent sign -> %
# must say: quote/quote to open/close quote, space to insert space within a quote
def converter(query):
    # conversions here
    query = query.lower()

    query = query.replace("so what", "select")
    query = query.replace("iowa id", "aisle_id")
    query = query.replace(" isles", " aisles")
    query = query.replace(" isle", " aisle")
    query = query.replace("i'll", "aisle")
    query = query.replace("equals", "=")
    query = query.replace("open parentheses ", "(")
    query = query.replace(" close parentheses", ")")
    query = query.replace("average ", "avg")
    query = query.replace("is greater than",">")
    query = query.replace("is less than", "<")
    query = query.replace("is greater than or equal to", ">=")
    query = query.replace("is less than or equal to", "<=")
    query = query.replace("greater than", ">")
    query = query.replace("less than", "<")
    query = query.replace("greater than or equal to", ">=")
    query = query.replace("less than or equal to", "<=")
    query = query.replace("aisle id", "aisle_id")
    query = query.replace("department id", "department_id")
    query = query.replace("product id", "product_id")
    query = query.replace("order id", "order_id")
    query = query.replace("user id", "user_id")
    query = query.replace("product name", "product_name")
    query = query.replace("order number", "order_number")
    query = query.replace("order day of week", "order_dow")
    query = query.replace("order dow", "order_dow")
    query = query.replace("order hour", "order_hour")
    query = query.replace("days since prior order", "days_since_prior_order")
    query = query.replace("add to cart", "add_to_cart")
    query = query.replace("ascending", "asc")
    query = query.replace("descending", "desc")
    query = query.replace("order products", "order_products")


    list_query = query.split()
    where_stoppers = ["and", "or", "order by", "group by", "union"]

    # quotation handling
    while "quote" in list_query:
        quote_index = list_query.index("quote")
        if "quote" not in list_query[quote_index+1:]:
            return "error"

        unquote_index = list_query[quote_index+1:].index("quote") + quote_index + 1

        list_query[quote_index] = "\'"
        list_query[unquote_index] = "\'"

        while "space" in list_query[quote_index:unquote_index]:
            list_query[list_query.index("space")] = " "

        list_query[quote_index: unquote_index + 1] = [''.join(list_query[quote_index: unquote_index + 1])]

    if "order" in list_query:
        order_index = list_query.index("order")
        if list_query[order_index + 1] == "by":
            list_query[order_index: order_index + 2] = [' '.join(list_query[order_index: order_index + 2])]

    if "group" in list_query:
        group_index = list_query.index("group")
        if list_query[group_index + 1] == "by":
            list_query[group_index: group_index + 2] = [' '.join(list_query[group_index: group_index + 2])]

    query = " ".join(list_query)
    query = query + ";"
    return query


def execute_query(query):
    db = mysql.connect(
        host="localhost",
        user="root",
        passwd="ARcs527p",
        auth_plugin='mysql_native_password'
    )

    # print(db)

    cursor = db.cursor()
    cursor.execute("use instacart")

    try:
        cursor.execute(query)
        rows = cursor.fetchall()

        root = Tk()
        title = "Query: " + query + " Rows: " + str(len(rows))
        root.title(title)

        f = Frame(root)
        f.pack()

        xscrollbar = Scrollbar(f, orient=HORIZONTAL)
        xscrollbar.grid(row=1, column=0, sticky=N + S + E + W)

        yscrollbar = Scrollbar(f)
        yscrollbar.grid(row=0, column=1, sticky=N + S + E + W)

        columns = cursor.description
        col_tuple = ()
        for column in columns:
            col_tuple = col_tuple + (column[0],)

        tree = ttk.Treeview(f,
                            columns=col_tuple,
                            show='headings',
                            xscrollcommand=xscrollbar.set,
                            yscrollcommand=yscrollbar.set)

        tree.grid(row=0, column=0)

        for col in col_tuple:
            tree.heading(col, text=col)

        xscrollbar.config(command=tree.xview)
        yscrollbar.config(command=tree.yview)

        # insert the actual query result rows here
        for row in rows:
            # text.insert(END, row)
            # text.insert(END, '\n')
            tree.insert("", "end", values=row)
        root.mainloop()

    except mysql.Error as e:
        prompt.configure(text=e)


def clicked():
    prompt.configure(text="Say something...")

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    guess = recognize_speech_from_mic(recognizer, microphone)
    if guess["error"]:
        prompt.configure(text=("ERROR: {}".format(guess["error"])))
    elif not guess["transcription"]:
        prompt.configure(text="I didn't catch that. Please try again\n")
        return

    # show the user the transcription
    prompt.configure(text=("You said: {}".format(guess["transcription"])))

    # determine if query is acceptable
    # valid_query = validator(guess["transcription"])
    valid_query = True

    if valid_query:
        query = converter(guess["transcription"])
        prompt.configure(text="Fetching query...")
        your_input = "Your Query: " + query
        user_input.configure(text=your_input)

        execute_query(query)

        # send query
        return
    else:
        your_input = "Your Input: " + guess["transcription"]
        user_input.configure(text=your_input)
        prompt.configure(text="Sorry, please say a valid query.")
        return


if __name__ == "__main__":

    # execute_query("select * from products where product_id < 100")
    window = Tk()
    window.title("Query Processing")

    prompt = Label(window, text="Press the button to record your query.")
    prompt.grid(column=0, row=0)

    record = Button(window, text="Record", command=clicked, bg="red")

    record.grid(column=0, row=1)

    user_input = Label(window, text="")
    user_input.grid(column=0, row=3)

    container = Frame(window)
    canvas = Canvas(container)
    scrollbar = Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas)

    window.mainloop()





