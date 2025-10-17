class AgeCheck
{
    static public void Check()
    {
        Console.WriteLine("Age Verification");
        Console.WriteLine("----------------");
        Console.WriteLine("Enter your name");
        string rawname = Console.ReadLine() ?? "";
        string name = string.IsNullOrWhiteSpace(rawname) ? "Doggo" : rawname;
        Console.WriteLine("Enter your age:");
        int input = int.Parse(Console.ReadLine() ?? "1");
        Console.WriteLine($"Welcome {name} !");
        if (input < 18)
        {
            Console.WriteLine("You are a minor.");
        }
        else
        {
            Console.WriteLine("You are major.");
        }
    }
}