namespace Whisperer.Services
{
    using Markdig;
    using Microsoft.AspNetCore.Components;
    using Whisperer.Extensions;

    public class MarkdownService : IMarkdownService
    {
        private readonly MarkdownPipeline pipeline;

        public MarkdownService()
        {
            pipeline = new MarkdownPipelineBuilder().UseAdvancedExtensions()
                                                         .Use<TargetLinkExtension>()
                                                         .Build();
        }

        public MarkupString ToHtml(string content)
        {
            return (MarkupString)Markdown.ToHtml(content, pipeline);
        }
    }
}
