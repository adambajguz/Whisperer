namespace Whisperer.Configurations
{
    public sealed class SuggestionsConfiguration
    {
        public string? ApiUri { get; init; }

        public int MinCount { get; init; }
        public int MaxCount { get; init; }
        public int DefaultCount { get; init; }
    }
}
