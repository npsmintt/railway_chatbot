import mysql.connector
import os

def insert_file_data_from_folder(folder_path):
    try:
        # Establish a connection to the database
        db_connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="234236238",
            database="ChatbotContingency"
        )

        cursor = db_connection.cursor()

        for document_name in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, document_name)):
                select_query = "SELECT COUNT(*) FROM document WHERE document_name = %s"
                cursor.execute(select_query, (document_name,))
                result = cursor.fetchone()[0]

                if result > 0:
                    with open(os.path.join(folder_path, document_name), "rb") as file:
                        document_file = file.read()

                    update_query = "UPDATE document SET document_file = %s WHERE document_name = %s"
                    cursor.execute(update_query, (document_file, document_name))
                    db_connection.commit()

                    print(f"File data inserted successfully for {document_name}")

    except mysql.connector.Error as error:
        print(f"Error inserting file data: {error}")

    finally:
        if 'db_connection' in locals():
            cursor.close()
            db_connection.close()

insert_file_data_from_folder('/Users/mac/Desktop/Study/Artificial_Intelligence/CW2/cw2_chatbot_contingencies/contingency_doc')
