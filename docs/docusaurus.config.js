// @ts-check

const lightCodeTheme = require("prism-react-renderer/themes/github");
const darkCodeTheme = require("prism-react-renderer/themes/dracula");

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: "RDS-NG Documentation",
  tagline: "Everything about the next generation version of RDS",
  favicon: "img/favicon.ico",

  // Set the production url of your site here
  url: "https://research-data-services.org",
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: "/",

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: "University of Muenster", // Usually your GitHub org/user name.
  projectName: "rds-ng-docs", // Usually your repo name.

  onBrokenLinks: "throw",
  onBrokenMarkdownLinks: "warn",

  i18n: {
    defaultLocale: "en",
    locales: ["en"],
  },

  presets: [
    [
      "classic",
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve("./sidebars.js"),
        },
        theme: {
          customCss: require.resolve("./src/css/custom.css"),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: "img/docusaurus-social-card.jpg",
      navbar: {
        title: "RDS-NG",
        logo: {
          alt: "RDS-NG",
          src: "img/logo.svg",
        },
        items: [
          {
            type: "dropdown",
            label: "Code Reference",
            position: "right",
            items: [
              {
              type: "docSidebar",
              sidebarId: "backendSidebar",
              label: "Python (Backend)",
            },
            {
              type: "docSidebar",
              sidebarId: "frontendSidebar",
              label: "TypeScript (Frontend)",
            },
          ]
          }
          
        ],
      },
      footer: {
        style: "dark",
        links: [],
        copyright: `Copyright © ${new Date().getFullYear()} University of Muenster.`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
      },
    }),

  plugins: [
    [
      "docusaurus-plugin-typedoc",

      // Plugin / TypeDoc options
      {
        entryPoints: ["../src/frontend/src/", "../src/common/web/"],
        exclude: "../src/frontend/src/vue-shim.d.ts",
        entryPointStrategy: 'expand',
        tsconfig: "../src/frontend/tsconfig.json",
        out: "reference/frontend",
        //readme: "", // currently deleted in refresh_reference.sh after build
        //readmeTitle: "", // only applies to the Readme, set `name` for README, ToC etc. title
        sidebar: {
          categoryLabel: "Frontend",
          position: 0,
        },
      },
    ],
  ],
};

module.exports = config;
