export function nowParts(timeZone = process.env.TIMEZONE || "Asia/Taipei") {
  const formatter = new Intl.DateTimeFormat("en-CA", {
    timeZone,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    hour12: false
  });

  const values = Object.fromEntries(
    formatter.formatToParts(new Date()).map((part) => [part.type, part.value])
  );

  return {
    date: `${values.year}-${values.month}-${values.day}`,
    hour: values.hour,
    minute: values.minute,
    timeZone
  };
}

export function isScheduledTime(hour, minute, timeZone) {
  const current = nowParts(timeZone);
  return current.hour === hour && current.minute === minute;
}
