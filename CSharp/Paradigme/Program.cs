using System;

main();

static void main()
{
    // AgeCheck.Check();
    //AverageGrade avgGrade = new AverageGrade();
    //avgGrade.AddGrade(100);
    //avgGrade.AddGrade(0);
    //Console.WriteLine($"Average Grade: {avgGrade.CalculateAverage()}");
}
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

class AverageGrade()
{
    private List<int> grades = new List<int>();
    public void AddGrade(int grade)
    {
        grades.Add(grade);
    }
    public double CalculateAverage()
    {
        if (grades.Count == 0) return 0;
        return grades.Average();
    }
}
