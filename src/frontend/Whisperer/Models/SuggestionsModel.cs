using System.Text.Json.Serialization;

namespace Whisperer.Models
{
    public class SuggestionsModel
    {
        [JsonPropertyName("predicted_words")]
        public string[]? PredictedWords { get; init; }
    }
}
