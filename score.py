import sqlite3
import os.path
import sys

class Scores:

    def __init__(self, test=False):

        # Connect to the high scores database
        if test:
            path = "test_scores.sqlite"
        else:
            path = "scores.sqlite"
        self.__connect(path)

        # Create the table if it doesn't exist
        self.__query_table('''
        CREATE TABLE IF NOT EXISTS Scores (
            points SMALLINT NOT NULL,
            name VARCHAR(24) NOT NULL,
            mode VARCHAR(16) NOT NULL,
            difficulty VARCHAR(32) NOT NULL
        );
        ''')


    def __connect(self, path):
        '''
        Will attempt to connect to database. Will try to create one if it can't.
        If it can't do that, it will ask the user to manually create one.
        :param path:
        :return:
        '''
        try:
            self.connection = sqlite3.connect(path)
            self.cursor = self.connection.cursor()
        except:
            if not os.path.exists(path):
                # Create it, and close it
                f = open(path, "w+")
                f.close()
                # And try again
                return self.__connect(path)
            else:
                print(f"No database exists, and could not create one.\nPlease create file in app directory called: {path}\nThen restart application.")
                raise

    def __query_table(self, sql, args=False):
        # Attempt to write to database
        try:
            if args is False:
                return self.cursor.execute(sql)
            else:
                return self.cursor.execute(sql, args)
        except:
            print(f"{sql[0:160]}\n\nDatabase could not execute with above query; error message:\n\n{sys.exc_info()[0]}")
            raise

    def get_highscores(self, mode="classic", difficulty=False):
        '''
        Gets the high scores for the mode
        :param difficulty:
        :return:
        '''

        if difficulty is False:
            # Get total high scores for all gamemodes
            return self.__query_table("""
                                SELECT name, points
                                FROM Scores
                                ORDER BY points desc
                            """, (difficulty))

        # Else, get it for a particular difficulty.
        # Guard: Difficulty must be in expected difficulties
        expected_difficulties = ("test", "beginner", "intermediate", "expert")
        if difficulty not in expected_difficulties:
            return False

        data = self.__query_table(f"""
                    SELECT name, points
                    FROM Scores
                    WHERE difficulty LIKE '{difficulty}'
                    AND mode LIKE '{mode}'
                    ORDER BY points desc
                """)

        score_list = []
        for row in data:
            score_list.append(row)

        self.connection.close()

        return score_list

    def clear_testscores(self):
        '''
        Deletes test data from database
        :return:
        '''
        self.__query_table(f"""
                DELETE FROM Scores
                WHERE difficulty LIKE 'test'
            """)


    def write_highscore(self, name, points, mode, difficulty):
        '''
        Accepts high score dict
        :param new_score: {name: "", difficulty: "", points: 0}
        :return: successful(Bool)
        '''

        # Guards: Arguments must exist
        if not name:
            return
        if not difficulty:
            return
        if not points:
            return

        # Guard: Difficulty must be in expected difficulties
        expected_difficulties = ("test", "beginner", "intermediate", "expert")
        if difficulty not in expected_difficulties:
            return False

        self.__query_table(f"""
            INSERT INTO Scores
            VALUES (?, ?, ?, ?)
        """, (points, name, mode, difficulty))

        return True

    def __sanitise(self, s):
        return

    def save(self):
        try:
            self.connection.commit()
            return self.connection.close()
        except sqlite3.ProgrammingError:
            print("Warning: Attempted to close already closed database.")
