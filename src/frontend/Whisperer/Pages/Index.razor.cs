namespace Whisperer.Pages
{
    using System;
    using System.Net.Http;
    using System.Net.Http.Json;
    using System.Threading.Tasks;
    using Microsoft.AspNetCore.Components;
    using Microsoft.Extensions.Options;
    using Whisperer.Configurations;
    using Whisperer.Models;
    using Whisperer.Services;

    public partial class Index : ComponentBase
    {
        private const string DefaultCode = @"I have a book.";

        private bool IsInitialized { get; set; }

        [Inject] private MonacoEditorService MonacoEditor { get; set; } = default!;
        [Inject] private HttpClient Client { get; set; } = default!;

        private string[]? Completions { get; set; } = new[] { "test", "plain-text", "green" };

        private SuggestionPreferences Preferences { get; set; } = new();

        [Inject] private IOptions<SuggestionsConfiguration> _SuggestionsConfiguration { get; init; } = default!;
        private SuggestionsConfiguration SuggestionsConfiguration => _SuggestionsConfiguration.Value;

        protected override void OnParametersSet()
        {
            Preferences = new() { Count = SuggestionsConfiguration.DefaultCount };
        }

        protected override async Task OnAfterRenderAsync(bool firstRender)
        {
            await base.OnAfterRenderAsync(firstRender);

            if (firstRender)
            {
                await MonacoEditor.InitializeAsync("container", DefaultCode, "plain", "hc-black", false, true);

                await Task.Delay(1100);
                IsInitialized = true;
                StateHasChanged();
            }
        }

        private async Task ClearAsync()
        {
            await MonacoEditor.SetTextAsync("container", string.Empty);
        }

        private async Task ToggleLineNumbersAsync()
        {
            await MonacoEditor.ToggleLineNumbersVisibility("container");
        }

        private async Task TypeText(string str)
        {
            await MonacoEditor.TypeTextAsync("container", " " + str);
        }

        private async void RefreshCompletions(SuggestionPreferences preferences)
        {
            if (preferences.Count <= 0)
                preferences.Count = 5;

            string apiUri = SuggestionsConfiguration.ApiUri ?? string.Empty;
            string text = await MonacoEditor.GetTextAsync("container");

            var response = await Client.GetAsync($"{apiUri}/predict?sentence={text}&count={preferences.Count}");
            if (response.IsSuccessStatusCode)
            {
                var model = await response.Content.ReadFromJsonAsync<SuggestionsModel>();

                Completions = model?.PredictedWords ?? Array.Empty<string>();
            }
        }
    }
}
