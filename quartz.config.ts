import { QuartzConfig } from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"

const config: QuartzConfig = {
  configuration: {
    pageTitle: "デライト LLM Wiki",
    pageTitleSuffix: "",
    enableSPA: true,
    enablePopovers: true,
    analytics: null,
    locale: "ja-JP",
    baseUrl: "nishio.github.io/llm-wiki-about-delite",
    ignorePatterns: [
      "raw",
      "tmp",
      "tools",
      "node_modules",
      "public",
      "private",
      "templates",
      ".obsidian",
      ".claude",
      ".github",
      "quartz",
      "quartz.config.ts",
      "quartz.layout.ts",
      "memo.txt",
      "second.txt",
      "pnpm-lock.yaml",
      "package.json",
      "tsconfig.json",
      "tsconfig.tsbuildinfo",
      "CLAUDE.md",
      "init.txt"
    ],
    defaultDateType: "modified",
    theme: {
      fontOrigin: "googleFonts",
      cdnCaching: true,
      typography: {
        header: "Noto Serif JP",
        body: "Noto Sans JP",
        code: "IBM Plex Mono"
      },
      colors: {
        lightMode: {
          light: "#f7f5ef",
          lightgray: "#ddd8cb",
          gray: "#8f8a7c",
          darkgray: "#3d3a31",
          dark: "#1f1e19",
          secondary: "#1d5c4d",
          tertiary: "#a56a2a",
          highlight: "rgba(29, 92, 77, 0.12)",
          textHighlight: "#ffef9a"
        },
        darkMode: {
          light: "#161613",
          lightgray: "#323129",
          gray: "#666356",
          darkgray: "#d8d4c8",
          dark: "#f4f1e8",
          secondary: "#78c2af",
          tertiary: "#d6a15f",
          highlight: "rgba(120, 194, 175, 0.16)",
          textHighlight: "#8f7a10"
        }
      }
    }
  },
  plugins: {
    transformers: [
      Plugin.FrontMatter(),
      Plugin.CreatedModifiedDate({
        priority: ["frontmatter", "git", "filesystem"]
      }),
      Plugin.SyntaxHighlighting({
        theme: {
          light: "github-light",
          dark: "github-dark"
        },
        keepBackground: false
      }),
      Plugin.ObsidianFlavoredMarkdown({ enableInHtmlEmbed: false }),
      Plugin.GitHubFlavoredMarkdown(),
      Plugin.TableOfContents(),
      Plugin.CrawlLinks({ markdownLinkResolution: "shortest" }),
      Plugin.Description()
    ],
    filters: [Plugin.RemoveDrafts()],
    emitters: [
      Plugin.AliasRedirects(),
      Plugin.ComponentResources(),
      Plugin.ContentPage(),
      Plugin.FolderPage(),
      Plugin.TagPage(),
      Plugin.ContentIndex({
        enableSiteMap: true,
        enableRSS: true
      }),
      Plugin.Assets(),
      Plugin.Static(),
      Plugin.Favicon(),
      Plugin.NotFoundPage(),
      Plugin.CustomOgImages()
    ]
  }
}

export default config
