<<<<<<< HEAD
﻿using System;
using System.Collections.Generic;
using System.Data.SQLite;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

// See https://aka.ms/new-console-template for more information
namespace CoffeeDataConnector
{
    class DataConnector
    {
        static void Main(string[] args)
        {
            SQLiteConnection sqlite_conn;
            sqlite_conn = CreateConnection();
            ReadAllCustomerData(sqlite_conn);
            ReadAllOrders(sqlite_conn);
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
    }
}