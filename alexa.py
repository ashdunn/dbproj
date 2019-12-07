import mysql.connector as mysql
import speech_recognition as sr


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
    query = query.replace("equals", "=")
    query = query.replace("open parentheses ", "(")
    query = query.replace(" close parentheses", ")")
    query = query.replace("average ", "avg")
    query = query.replace("greater than",">")
    query = query.replace("less than", "<")
    query = query.replace("greater than or equal to", ">=")
    query = query.replace("less than or equal to", "<=")


    list_query = query.lower().split()
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

    print(db)


if __name__ == "__main__":

    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone(device_index=2)


    # show instructions and wait 3 seconds before starting the game
    print("Please say a query")
    input("Press Enter to continue...")

    for i in range(10):
        # get the guess from the user
        # if a transcription is returned, break out of the loop and
        #     continue
        # if no transcription returned and API request failed, break
        #     loop and continue
        # if API request succeeded but no transcription was returned,
        #     re-prompt the user to say their guess again. Do this up
        #     to PROMPT_LIMIT times
        for j in range(10):
            guess = recognize_speech_from_mic(recognizer, microphone)
            if guess["transcription"]:
                break
            if not guess["success"]:
                break
            print("I didn't catch that. What did you say?\n")

        # if there was an error, stop the game
        if guess["error"]:
            print("ERROR: {}".format(guess["error"]))
            break

        # show the user the transcription
        print("You said: {}".format(guess["transcription"]))

        # determine if guess is correct and if any attempts remain
        valid_query = validator(guess["transcription"])

        # determine if the user has won the game
        # if not, repeat the loop if user has more attempts
        # if no attempts left, the user loses the game
        if valid_query:
            query = converter(guess["transcription"])
            print("Query Form: {}".format(query))
            print("Fetching query...")

            ans = execute_query(query)

            # send query
            break
        else:
            print("Sorry, please say a valid query")