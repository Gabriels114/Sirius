function useFlightProgress({departure, arrival, minutes}:{departure:string, arrival:string, minutes: number}) {
    if (!departure || !arrival) return 0;

    const departureTime = convertToMinutes(departure);
    const arrivalTime = convertToMinutes(arrival);
    const totalFlightTime = arrivalTime - departureTime;
  
    if (totalFlightTime <= 0) return 0;
  
    const percentage = (minutes / totalFlightTime) * 100;
    return Math.min(percentage, 100); 
    }
  
  function convertToMinutes(time: string) {
    const [hh, mm, ss] = time.split(":").map(Number);
    return hh * 60 + mm + ss / 60;
  }

export default useFlightProgress;
