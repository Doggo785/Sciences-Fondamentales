class Item
{
    private string name;
    private int quantity;
    public Item(string name, int quantity)
    {
        this.name = name;
        this.quantity = quantity;
    }
    public string Name
    {
        get => name;
        set
        {
            if (string.IsNullOrWhiteSpace(value))
                throw new ArgumentException("Item name cannot be null or empty.");
            name = value;
        }
    }
    public int Quantity
    {
        get => quantity;
        set
        {
            if (value < 0)
                throw new ArgumentException("Item name cannot be null or empty.");
            quantity = value;
        }
    }

}

class Inventory
{
    private List<Item> items;
    public Inventory()
    {
        items = new List<Item>();
    }
    public void AddItem(Item item)
    {
        items.Add(item);
    }
    public void RemoveItem(Item item) {
        items.Remove(item);
    }
    public void DisplayItems()
    {
        foreach (var item in items)
        {
            Console.WriteLine($"Item: {item.Name}, Quantity: {item.Quantity}");
        }
    }
}



