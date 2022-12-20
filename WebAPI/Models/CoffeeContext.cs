namespace WebAPI.Models;
using Microsoft.EntityFrameworkCore;
public class CoffeeContext : DbContext
{
    public CoffeeContext(DbContextOptions<CoffeeContext> options)
        : base(options)
    {
    }

    public DbSet<coffeeOrder> coffeeOrder { get; set; } = null!;
}