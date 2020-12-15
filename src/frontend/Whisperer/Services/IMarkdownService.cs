namespace Whisperer.Services
{
    using Microsoft.AspNetCore.Components;

    public interface IMarkdownService
    {
        MarkupString ToHtml(string content);
    }
}
