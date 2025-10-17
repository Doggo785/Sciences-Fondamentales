class AverageGrade
{
    private List<int> grades = new List<int>();

    public AverageGrade()
    {
        Console.WriteLine("Average Grade Calculation");
        Console.WriteLine("-------------------------");
        Console.WriteLine("Enter grades one by one. Type 'done' to finish.");
        string input = Console.ReadLine() ?? "done";
        while (input.ToLower() != "done")
        {
            if (int.TryParse(input, out int grade))
            {
                AddGrade(grade);
            }
            else
            {
                Console.WriteLine("Invalid input. Please enter a valid grade or 'done' to finish.");
            }
            input = Console.ReadLine() ?? "done";
        }
        Console.WriteLine($"Average Grade: {CalculateAverage()}");
    }
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