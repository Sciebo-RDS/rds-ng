import { definePreset, palette } from "@primevue/themes";
import Aura from "@primevue/themes/aura";

import { ThemeSettingIDs } from "../../settings/ThemeSettingIDs";
import { Configuration } from "../../utils/config/Configuration";

/**
 * Creates the theme for the application.
 */
export function theme(config: Configuration): any {
    return definePreset(Aura, {
        semantic: {
            primary: palette(config.value<string>(ThemeSettingIDs.PrimaryColor)),
            focusRing: {
                width: "0px",
                style: "solid",
                color: "transparent"
            },
            colorScheme: {
                light: {
                    surface: palette(config.value<string>(ThemeSettingIDs.LightSurfaceColor))
                },
                dark: {
                    surface: palette(config.value<string>(ThemeSettingIDs.DarkSurfaceColor))
                }
            }
        },
        components: {
            fieldset: {
                colorScheme: {
                    light: {
                        padding: "0",
                        borderRadius: "0",
                        legend: { padding: "0.5rem 0.5rem 0.5rem 0" },
                        content: { padding: "0.25rem" }
                    },
                    dark: {
                        padding: "0",
                        borderRadius: "0",
                        legend: { padding: "0.5rem 0.5rem 0.5rem 0" },
                        content: { padding: "0.25rem" }
                    }
                }
            }
        },
        extend: {
            rds: {
                colorScheme: {
                    highlight: palette(config.value<string>(ThemeSettingIDs.LightHighlightColor)) // TODO: Dark mode support
                }
            }
        }
    });
}
