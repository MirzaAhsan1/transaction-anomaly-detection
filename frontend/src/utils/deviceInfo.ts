import { UAParser } from "ua-parser-js";

export interface DeviceInfo {
    browser: string;
    browser_version: string;
    operating_system: string;
    os_version: string;
    device_type: string;
    language: string;
    timezone: string;
    screen_width: number;
    screen_height: number;
    user_agent: string;
}

export const getDeviceInfo = (): DeviceInfo => {
    const parser = new UAParser();

    const result = parser.getResult();

    return {
        browser: result.browser.name || "Unknown",
        browser_version: result.browser.version || "",

        operating_system: result.os.name || "Unknown",
        os_version: result.os.version || "",

        device_type: result.device.type
            ? result.device.type.charAt(0).toUpperCase() +
            result.device.type.slice(1)
            : "Desktop",

        language: navigator.language,

        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,

        screen_width: window.screen.width,

        screen_height: window.screen.height,

        user_agent: navigator.userAgent,
    };
};