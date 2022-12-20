namespace WebAPI.Models;
using Microsoft.EntityFrameworkCore;
public class coffeeOrder{
    public long orderID {get; set; }
    public long customerID {get; set;}
    // public list<CupOfCoffee> coffeeList = new list<CupOfCoffee>();

    public class CupOfCoffee{
        public long coffeeID {get; set;}
        public string? coffeeName {get; set;}
        public string? coffeeSize {get; set;}
        // public list<CoffeeExtras> extrasList = new list<CoffeeExtras>();

        public class CoffeeExtras{
            public int extraCoffeeID { get; set; }
            public string? extraName { get; set; }
            public int amount {get; set;}
        }
    }
}