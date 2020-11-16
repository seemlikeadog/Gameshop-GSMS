from datetime import date
import pymysql
from pymysql.cursors import DictCursor


class SQLExecutor:
    """
    A controller that is used to interact with MYSQL DB.
    It is used to execute sql queries and retrieve results from MYSQL DB
    """

    def __init__(self, host, username, password, database):
        """

        :param host:   hostname of db
        :param username:    username of db
        :param password:    password of db
        :param database:    database that will use

        :type host: str
        :type username: str
        :type password: str
        :type database: str
        """
        self.host = host
        self.username = username
        self.password = password
        self.database = database

    def connection_test(self) -> bool:
        """
        :return: True if connection test success, False otherwise
        """
        try:
            connection = pymysql.connect(self.host, self.username, self.password, self.database)

            with connection.cursor() as cursor:
                sql = "SELECT VERSION()"
                cursor.execute(sql)

                result = cursor.fetchone()
                if result:
                    pass
                else:
                    return False

        except pymysql.err.ProgrammingError:
            print('A DB error caught')
        finally:
            connection.close()
            return True

    def select_game_by_id(self, id: str) -> tuple:
        """
        :param id: the id of the selected name
        :return: a tuple that contains all info of the selected game
        """

        try:
            connection = pymysql.connect(self.host, self.username, self.password, self.database)

            with connection.cursor() as cursor:
                sql = "SELECT * FROM Game WHERE game_id = %s"
                cursor.execute(sql, id)

                result = cursor.fetchone()

        except pymysql.err.ProgrammingError:
            print('A DB error caught')
        finally:
            return result
            connection.close()

    def select_game_by_name(self, name: str = "") -> tuple:
        """
        :param name: the name of the selected name
        :return: a tuple that contains all info of the selected game
        """
        try:
            connection = pymysql.connect(self.host, self.username, self.password, self.database)

            with connection.cursor() as cursor:

                sql = "SELECT * FROM Game WHERE game_name LIKE %s"
                # ('%'+name+'%',) is semantically equal to "%name%"
                game_name = "'%" + name + "%'"
                print(game_name)
                cursor.execute(sql, game_name)
                result = cursor.fetchall()

        except pymysql.err.ProgrammingError:
            print('A DB error caught')
        except ConnectionError:
            print("Unknown Connection Error")
        finally:
            connection.close()
            return result

    def check_store_address(self, store_id: str) -> tuple:
        """
        :param store_id: the store id
        :return: a tuple contains the store information
        """
        try:
            connection = pymysql.connect(self.host, self.username, self.password, self.database)
            with connection.cursor() as cursor:
                sql = "SELECT * FROM Store WHERE store_id = %s"
                cursor.execute(sql, store_id)
                result = cursor.fetchone()

        except pymysql.err.ProgrammingError:
            print('A DB error caught')
        except ConnectionError:
            print("Unknown Connection Error")
        finally:
            connection.close()
            return result

    def check_game_copies(self, game_id: str) -> tuple:
        """
        :param game_id: the game id
        :return: list num of copies of a game within a store
        """
        try:
            connection = pymysql.connect(self.host, self.username, self.password, self.database)
            with connection.cursor() as cursor:
                sql = "SELECT Has_Games.store_id,Store.store_name, Has_Games.game_id,Game.game_name,num_of_copies \
                        FROM Has_Games, Store, Game \
                        WHERE Store.store_id = Has_Games.store_id \
                        and Game.game_id = Has_Games.game_id \
                        and Has_Games.game_id = %s"
                cursor.execute(sql, game_id)
                result = cursor.fetchone()

        except pymysql.err.ProgrammingError:
            print('A DB error caught')
        except ConnectionError:
            print("Unknown Connection Error")
        finally:
            connection.close()

            return result if result else ('No Results Found',)

    def check_customer_memberships(self, customer_id: str) -> tuple:
        """
        :param customer_id: the customer id
        :return: a tuple with customer info with hes/her corresponding membership
        """
        try:
            connection = pymysql.connect(self.host, self.username, self.password, self.database)
            with connection.cursor() as cursor:
                sql = "select Customer.customer_id, fname, lname, membership_type \
                      from Customer, Customer_Membership,Membership \
                      where Customer.customer_id = Customer_Membership.customer_id \
                      and Membership.membership_id = Customer_Membership.membership_id \
                      and Customer.customer_id = %s"
                cursor.execute(sql, customer_id)
                result = cursor.fetchone()

        except pymysql.err.ProgrammingError:
            print('A DB error caught')
        except ConnectionError:
            print("Unknown Connection Error")
        finally:
            connection.close()

            return result if result else ('No Results Found',)

    def list_developer_games(self, developer_id: str) -> tuple:
        """
        List all games that published by a specific developer
        :param developer_id: The developer id
        :return: a tuple contain a list of games that the developer published
        """
        try:
            connection = pymysql.connect(self.host, self.username, self.password, self.database)
            with connection.cursor() as cursor:
                sql = "select D.developer_id, developer_name, G.game_id, game_name, release_date, genre, platform, price \
                        from Game as G, Developer as D, Published_Games as P \
                        where G.game_id = P.game_id \
                        and D.developer_id = P.developer_id \
                        and D.developer_id = %s"
                cursor.execute(sql, developer_id)
                result = cursor.fetchall()

        except pymysql.err.ProgrammingError:
            print('A DB error caught')
        except ConnectionError:
            print("Unknown Connection Error")
        finally:
            connection.close()
            return result if result else ('No Results Found',)

    def list_all_published_games(self):
        """
        list all games that published by all developer
        :return: a tuple that list all developers with all games they published
        """
        try:
            connection = pymysql.connect(self.host, self.username, self.password, self.database)
            with connection.cursor() as cursor:
                sql = "select developer_name, game_name,release_date, genre, price,platform \
                        from Published_Games, Developer, Game \
                        where Published_Games.developer_id = Developer.developer_id \
                        and Published_Games.game_id = Game.game_id \
                        ORDER BY developer_name"
                cursor.execute(sql)
                result = cursor.fetchall()

        except pymysql.err.ProgrammingError:
            print('A DB error caught')
        except ConnectionError:
            print("Unknown Connection Error")
        finally:
            connection.close()
            return result if result else ('No Results Found',)

    def list_all_customer_memberships(self):
        """
        list all customers and their memberships
        :return:
        """
        try:
            connection = pymysql.connect(self.host, self.username, self.password, self.database)
            with connection.cursor() as cursor:
                sql = "select fname,lname,membership_type \
                        from Customer_Membership as R,Customer as C,Membership as M \
                        where R.membership_id = M.membership_id \
                        and R.customer_id = C.customer_id \
                        ORDER BY C.customer_id"
                cursor.execute(sql)
                result = cursor.fetchall()

        except pymysql.err.ProgrammingError:
            print('A DB error caught')
        except ConnectionError:
            print("Unknown Connection Error")
        finally:
            connection.close()
            return result if result else ('No Results Found',)

    def list_game_by_price(self, low: str, high: str) -> tuple:
        """
        List all games within a certain price range
        :param low: the lower bound of the price range
        :param high: the higher bound of the price range
        :return: a tuple contains all games within a specific price range
        """
        try:
            connection = pymysql.connect(self.host, self.username, self.password, self.database)
            with connection.cursor() as cursor:
                sql = "select game_name, price, release_date, genre,platform \
                        from Game, Has_Games,Store \
                        where Store.store_id = Has_Games.store_id \
                        and Game.game_id = Has_Games.game_id \
                        and price between %s and %s"
                cursor.execute(sql, low, high)
                result = cursor.fetchall()

        except pymysql.err.ProgrammingError:
            print('A DB error caught')
        except ConnectionError:
            print("Unknown Connection Error")
        finally:
            connection.close()
            return result if result else ('No Results Found',)

    def list_game_by_date(self, start_date: str, end_date: str) -> tuple:
        """
        List all games within a date range(The store has the game in store)
        :param start_date: The start date of the date boundary
        :param end_date: The end date of the date boundary
        :return: a tuple contains a list of games within a date range
        """

        try:
            connection = pymysql.connect(host=self.host, user=self.username, password=self.password,
                                         database=self.database)
            with connection.cursor() as cursor:
                sql = "select DISTINCT game_name, release_date, genre, platform, price \
                        from Game,Store, Has_Games \
                        where Store.store_id = Has_Games.store_id \
                        and Game.game_id = Has_Games.game_id \
                        and release_date between %s and %s"

                cursor.execute(sql, (start_date, end_date))
                result = cursor.fetchall()

        except pymysql.err.ProgrammingError:
            print('A DB error caught')
        except ConnectionError:
            print("Unknown Connection Error")
        finally:
            connection.close()
            return result if result else ('No Results Found',)

    def count_published_games_by_location(self, location: str) -> tuple:
        """
        num of games that published developer which located in the specific area
        :param location: a str contains location info
        :return: num of developers in the specific Area
        """
        try:
            connection = pymysql.connect(self.host, self.username, self.password, self.database)
            with connection.cursor() as cursor:
                sql = "select count(Game.game_id) as 'Number of Games' \
                        from Game, Published_Games, Developer \
                        where Developer.developer_id = Published_Games.developer_id \
                        and Game.game_id = Published_Games.game_id \
                        and address LIKE %s"
                location = "'%" + location + "%'"
                cursor.execute(sql, location)
                result = cursor.fetchall()

        except pymysql.err.ProgrammingError:
            print('A DB error caught')
        except ConnectionError:
            print("Unknown Connection Error")
        finally:
            connection.close()
            return result if result else ('No Results Found',)

    def num_of_copies(self, store_id: str) -> tuple:
        """
        Show how many game copies that a store has
        :param store_id: the given store id
        :return: a tuple showing the total num of game copies of a store
        """
        try:
            connection = pymysql.connect(self.host, self.username, self.password, self.database)
            with connection.cursor() as cursor:
                sql = "select Store.store_id,store_name,SUM(num_of_copies) as 'Num of Copies' \
                        from Store, Has_Games,Game \
                        where Store.store_id = Has_Games.store_id \
                        and Game.game_id = Has_Games.game_id \
                        and Store.store_id = %s \
                        GROUP BY Has_Games.store_id"
                cursor.execute(sql, store_id)
                result = cursor.fetchall()

        except pymysql.err.ProgrammingError:
            print('A DB error caught')
        except ConnectionError:
            print("Unknown Connection Error")
        finally:
            connection.close()
            return result if result else ('No Results Found',)

    def num_of_games(self, store_id: str) -> tuple:
        """
        List num of games that a store has
        :param store_id:
        :return:
        """
        try:
            connection = pymysql.connect(self.host, self.username, self.password, self.database)
            with connection.cursor() as cursor:
                sql = "select Store.store_id, COUNT(Has_Games.game_id) as 'Num of Games' \
                        from Store, Has_Games, Game \
                        where Store.store_id = Has_Games.store_id \
                        and Game.game_id = Has_Games.game_id \
                        and Store.store_id = %s \
                        GROUP BY Has_Games.store_id"
                cursor.execute(sql, store_id)
                result = cursor.fetchall()

        except pymysql.err.ProgrammingError:
            print('A DB error caught')
        except ConnectionError:
            print("Unknown Connection Error")
        finally:

            connection.close()
            return result if result else ('No Results Found',)

    def list_customer_history(self, customer_id, start, end):
        """

        :param customer_id: The given customer id
        :param start:   The start date of the date range
        :param end:     The end date of the date range
        :return:        a tuple contains the list of customer purchase history
        """
        try:
            connection = pymysql.connect(self.host, self.username, self.password, self.database)
            with connection.cursor() as cursor:
                sql = "select Store.store_id, store_name, fname,lname, purchaseDate \
                        from Store, Bought_Games, Customer, Game \
                        where Store.store_id = Bought_Games.store_id \
                        and Game.game_id = Bought_Games.game_id \
                        and (purchaseDate between %s and %s)\
                        and Customer.customer_id = %s"

                cursor.execute(sql, (customer_id, start, end))
                result = cursor.fetchall()

        except pymysql.err.ProgrammingError:
            print('A DB error caught')
        except ConnectionError:
            print("Unknown Connection Error")
        finally:
            connection.close()
            return result if result else ('No Results Found',)

    def add_game(self, game_name, release_date=date.today(), genre="", platform="", price="", availability=""):
        """
        Insert a game record into database
        :param game_name:       The game name
        :param release_date:    The release date of the name, use current date by default
        :param genre:           The genre of the game
        :param platform:        The platform that the game will be on: XBOX/PC/PlayStation
        :param price:           The price of the game
        :param availability:    The availability of the game
        :return:                print "INSERT SUCCESSFULLY" if insert succeed
        """

        try:
            connection = pymysql.connect(self.host, self.username, self.password, self.database)
            with connection.cursor() as cursor:
                sql = "INSERT INTO Game (game_name, release_date, genre, platform, price,availability) \
                        VALUES (%s,%s,%s,%s,%s,%s)"

                cursor.execute(sql, (game_name ,release_date, genre, platform, price,availability))

                connection.commit()
                print("INSERT SUCCESSFULLY")
        except pymysql.err.ProgrammingError:
            print('A DB error caught')
        except ConnectionError:
            print("Unknown Connection Error")
        finally:
            connection.close()

    def delete_game(self,game_id):
        """
        Delete a record from database by id
        :param game_id: the game_id of the game that need to be deleted
        :return: print "DELETE SUCCESSFULLY" if succeed
        """
        try:
            connection = pymysql.connect(self.host, self.username, self.password, self.database)
            with connection.cursor() as cursor:
                sql = "DELETE from Game WHERE game_id = %s"

                cursor.execute(sql, game_id)

                connection.commit()
                print("DELETE SUCCESSFULLY")
        except pymysql.err.ProgrammingError:
            print('A DB error caught')
        except ConnectionError:
            print("Unknown Connection Error")
        finally:
            connection.close()

    def update_game(self,game_id,game_name=None, release_date=None,
                    genre=None,platform=None,price=None,availability=None):
        """
        Update a game record according to its game id
        :param game_id: The game id
        :param game_name: The game name
        :param release_date: The game release date
        :param genre: The genre of the game
        :param platform: Which platform the game will be on
        :param price:   Price of the game
        :param availability: Currently null
        :return: Print "Update Successfully" to the terminal if success
        """
        try:
            connection = pymysql.connect(self.host, self.username, self.password, self.database)
            with connection.cursor() as cursor:
                sql = "UPDATE Game \
                      SET game_name = IFNULL(%s,game_name), \
                      release_date =  IFNULL(%s,release_date), \
                      genre = IFNULL(%s,genre), \
                      platform = IFNULL(%s,platform), \
                      price = IFNULL(%s, price) \
                      availability = IFNULL(%s,availability) \
                      WHERE game_id = %s"
                cursor.execute(sql, (game_name, release_date, genre, platform, price,availability, game_id))

                connection.commit()
                print("Update SUCCESSFULLY")
        except pymysql.err.ProgrammingError as e:
            print(f'A DB error caught\n {e}')
        except ConnectionError:
            print("Unknown Connection Error")
        finally:
            connection.close()

    def add_customer(self, fname:str, lname:str, address:str):
        """
        Add a customer record into database
        :param fname: Firstname
        :param lname: Lastname
        :param address: Customer address
        :return: print "INSERT SUCCESSFULLY" to the terminal
        """
        try:
            connection = pymysql.connect(self.host, self.username, self.password, self.database)
            with connection.cursor() as cursor:
                sql = "INSERT INTO Customer (fname, lname,address) \
                        VALUES (%s,%s,%s)"
                cursor.execute(sql, (fname, lname, address))
                connection.commit()
                print("INSERT SUCCESSFULLY")
        except pymysql.err.ProgrammingError as e:
            print(f'A DB error caught\n {e}')
        except ConnectionError:
            print("Unknown Connection Error")
        finally:
            connection.close()

    def delete_customer(self,customer_id):
        """
        Delete a customer record from database by id
        :param customer_id: the game_id of the customer that need to be deleted
        :return: print "DELETE SUCCESSFULLY" if succeed
        """
        try:
            connection = pymysql.connect(self.host, self.username, self.password, self.database)
            with connection.cursor() as cursor:
                sql = "DELETE from Customer WHERE customer_id = %s"
                cursor.execute(sql, customer_id)
                connection.commit()
                print("DELETE SUCCESSFULLY")
        except pymysql.err.ProgrammingError:
            print('A DB error caught')
        except ConnectionError:
            print("Unknown Connection Error")
        finally:
            connection.close()

    def update_customer(self,customer_id,fname=None, lname=None, address=None):
        """

        :param customer_id: customer_id indicate the record that need to be modified
        :param fname: firstname of customer
        :param lname: lastname
        :param address: customer address
        :return:
        """
        try:
            connection = pymysql.connect(self.host, self.username, self.password, self.database)
            with connection.cursor() as cursor:
                sql = "UPDATE Customer \
                      SET fname = IFNULL(%s,fname), \
                      lname = IFNULL(%s,lname), \
                      address = IFNULL(%s,address) \
                      WHERE customer_id = %s"
                cursor.execute(sql, (fname,lname,address,customer_id))
                connection.commit()
                print("UPDATE SUCCESSFULLY")
        except pymysql.err.ProgrammingError:
            print('A DB error caught')
        except ConnectionError:
            print("Unknown Connection Error")
        finally:
            connection.close()

    def add_developer(self,developer_name,address):
        """
        Add a developer
        :param developer_name: The developer name
        :param address: The developer address
        :return:
        """
        try:
            connection = pymysql.connect(self.host, self.username, self.password, self.database)
            with connection.cursor() as cursor:
                sql = "INSERT INTO Developer (developer_name, address) \
                        VALUES (%s,%s)"
                cursor.execute(sql, (developer_name,address))
                connection.commit()
                print("INSERT SUCCESSFULLY")
        except pymysql.err.ProgrammingError as e:
            print(f'A DB error caught\n {e}')
        except ConnectionError:
            print("Unknown Connection Error")
        finally:
            connection.close()

    def update_developer(self,developer_id,developer_name=None, address=None):


test = SQLExecutor(host="159.203.59.83", username="gamestop", password="Sn123456", database="gamestop")
print(test.list_game_by_date("2000-01-01", "2020-01-01"))
