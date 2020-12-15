﻿namespace Whisperer.Pages
{
    using System.Threading.Tasks;
    using Microsoft.AspNetCore.Components;
    using Whisperer.Services;

    public partial class Index
    {
        private const string DefaultCode = @"
Lorem ipsum, or lipsum as it is sometimes known, is dummy text used in laying out print, graphic or web designs. The passage is attributed to an unknown typesetter in the 15th century who is thought to have scrambled parts of Cicero's De Finibus Bonorum et Malorum for use in a type specimen book. It usually begins with:

“Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.”
The purpose of lorem ipsum is to create a natural looking block of text (sentence, paragraph, page, etc.) that doesn't distract from the layout. A practice not without controversy, laying out pages with meaningless filler text can be very useful when the focus is meant to be on design, not content.

The passage experienced a surge in popularity during the 1960s when Letraset used it on their dry-transfer sheets, and again during the 90s as desktop publishers bundled the text with their software. Today it's seen all around the web; on templates, websites, and stock designs. Use our generator to get your own, or read on for the authoritative history of lorem ipsum.
";

        private bool IsInitialized { get; set; }

        [Inject] private MonacoEditorService MonacoEditor { get; set; } = default!;

        protected override async Task OnAfterRenderAsync(bool firstRender)
        {
            await base.OnAfterRenderAsync(firstRender);

            if (firstRender)
            {
                await MonacoEditor.InitializeAsync("container", DefaultCode, "plain", "hc-black", false);

                await Task.Delay(1100);
                IsInitialized = true;
                StateHasChanged();
            }
        }


        private async Task ClearTerminalAsync()
        {
            await MonacoEditor.SetTextAsync("container", string.Empty);
        }

        private async Task ScrollToBottomAsync()
        {
            await MonacoEditor.ToggleLineNumbersVisibility("container");
        }
    }
}