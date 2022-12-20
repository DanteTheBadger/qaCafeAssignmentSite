using System;
using System.Collections.Generic;
using System.Data.SQLite;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CoffeeDataConnector
{
    class DataConnector
    {
        static void Main(string[] args)
        {
            SQLiteConnection sqlite_conn;
            sqlite_conn = CreateConnection();
            deleteCoffeeFromOrder(sqlite_conn, 2);
            sqlite_conn.Close();
        }

        static SQLiteConnection CreateConnection()
        {
            SQLiteConnection sqlite_conn = new SQLiteConnection("Data Source = database/qaCafeDatabase.db;Version=3;New=False;Compress=True;");
            try
            {
                sqlite_conn.Open();
            }
            catch
            {

            }
            return sqlite_conn;
        }
        static SQLiteDataReader ExecuteQuery(SQLiteConnection sqlite_conn, string queryString)
        {
            
            SQLiteDataReader sqliteDatareader;
            SQLiteCommand sqliteCmd;
            sqliteCmd = sqlite_conn.CreateCommand();
            sqliteCmd.CommandText = queryString;
            sqliteDatareader = sqliteCmd.ExecuteReader();
            return sqliteDatareader;
        }

        static void ReadAllCustomerData(SQLiteConnection sqlite_conn)
        {
            SQLiteDataReader sqliteDatareader;
            sqliteDatareader = ExecuteQuery(sqlite_conn, "select * from customer");
            while (sqliteDatareader.Read())
            {
                Console.Write($"{sqliteDatareader.GetValue(0)} {sqliteDatareader.GetValue(1)} {sqliteDatareader.GetValue(2)} \n");
            }
        }

        static void ReadAllOrders(SQLiteConnection sqlite_conn)
        {
            SQLiteDataReader sqliteDatareader;
            sqliteDatareader = ExecuteQuery(sqlite_conn, "select * from customerOrders");
            while (sqliteDatareader.Read())
            {
                Console.Write($"{sqliteDatareader.GetValue(0)} {sqliteDatareader.GetValue(1)}\n");
            }
        }
        static void ReadOrderByID(SQLiteConnection sqlite_conn, int orderID)
        {
            SQLiteDataReader sqliteDatareader;
            string queryString = 
            @$"SELECT customerOrders.orderID, orderCoffees.orderCoffeeID, orderCoffees.coffeeName, orderCoffees.cupName
            FROM customerOrders, orderCoffees
            WHERE customerOrders.orderID == orderCoffees.orderID
            AND customerOrders.orderID == {orderID};";
            sqliteDatareader = ExecuteQuery(sqlite_conn, queryString);
            while (sqliteDatareader.Read())
            {
                Console.Write($"{sqliteDatareader.GetValue(0)} {sqliteDatareader.GetValue(1)}\n");
            }
        }
        static void CreateOrder(SQLiteConnection sqlite_conn, int customerID)
        {
            SQLiteDataReader sqliteDatareader;
            string queryString = $"INSERT INTO customerOrders (customerID) VALUES ({customerID});";
            sqliteDatareader = ExecuteQuery(sqlite_conn, queryString);
            Console.Write(sqliteDatareader.RecordsAffected);
        }
        static void AddCoffeeToOrder(SQLiteConnection sqlite_conn, int orderID, string coffeeName, string cupSize)
        {
            SQLiteDataReader sqliteDatareader;
            string queryString = $"INSERT INTO orderCoffees (orderID, coffeeName, cupName) VALUES ({orderID}, '{coffeeName}', '{cupSize}');";
            sqliteDatareader = ExecuteQuery(sqlite_conn, queryString);
            Console.Write(sqliteDatareader.RecordsAffected);
        }
        static void UpdateOrderCoffee(SQLiteConnection sqlite_conn, int orderCoffeeID, string newCoffeeType, string newCupSize)
        {
            SQLiteDataReader sqliteDatareader;
            string queryString = $"SELECT * FROM orderCoffees WHERE orderCoffeeID == {orderCoffeeID};";
            sqliteDatareader = ExecuteQuery(sqlite_conn, queryString);
            // Checking if a new coffee type was passed
            if (sqliteDatareader.Read())
            {
                string[] updateValues = new string[2];
                if (newCoffeeType != sqliteDatareader.GetString(2) && newCoffeeType != "null")
                {
                    updateValues[0] = newCoffeeType;
                }
                else
                {
                    updateValues[0] = sqliteDatareader.GetString(2);
                }

                if (newCupSize != sqliteDatareader.GetString(3) && newCupSize != "null")
                {
                    updateValues[1] = newCupSize;
                }
                else
                {
                    updateValues[1] = sqliteDatareader.GetString(3);
                }
                string updateQueryString = $"UPDATE orderCoffees SET coffeeName = '{updateValues[0]}', cupName = '{updateValues[1]}' WHERE orderCoffeeID == {orderCoffeeID};";
                sqliteDatareader = ExecuteQuery(sqlite_conn, updateQueryString);
            }
        }

        static void deleteCoffeeFromOrder(SQLiteConnection sqlite_conn, int orderCoffeeID)
        {
            string firstDelete = $"DELETE FROM extrasToOrderCoffee WHERE orderCoffeeID = {orderCoffeeID};";
            string secondDelete = $"DELETE FROM orderCoffees WHERE orderCoffeeID = {orderCoffeeID};";
            ExecuteQuery(sqlite_conn, firstDelete);
            ExecuteQuery(sqlite_conn, secondDelete);
        }

        static void AddExtraToCoffee(SQLiteConnection sqlite_conn, int orderCoffeeID, string extraName, int amount)
        {
            SQLiteDataReader sqliteDatareader;
            string queryString = $"INSERT INTO extrasToOrderCoffee (orderCoffeeID, extraName, amount) VALUES ({orderCoffeeID}, '{extraName}', {amount});";
            sqliteDatareader = ExecuteQuery(sqlite_conn, queryString);
            Console.Write(sqliteDatareader.RecordsAffected);
        }
    }
}