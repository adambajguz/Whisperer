namespace Whisperer.Helpers
{
    using Microsoft.Extensions.Logging;

    public static class HtmlHelpers
    {
        public static string GetLogLevelAlias(LogLevel level)
        {
            return level switch
            {
                LogLevel.Trace => "trace",
                LogLevel.Debug => "debug",
                LogLevel.Information => "info",
                LogLevel.Warning => "warn",
                LogLevel.Error => "error",
                LogLevel.Critical => "critical",
                _ => level.ToString(),
            };
        }
    }
}
