import { useMemo } from "react";

const usePercentageColor = (percentage: number) => {
    const color = useMemo(() => {
        let red, green;

        if (percentage <= 50) {
            red = 255;
            green = Math.round((255 * percentage) / 50); 
        } else {
            red = Math.round(255 - (255 * (percentage - 50)) / 50); 
            green = 255;
        }
        return `rgb(${red}, ${green}, 0)`;
    }, [percentage]);

    return color;
}

export default usePercentageColor;
