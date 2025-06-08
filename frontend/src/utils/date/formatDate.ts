import { formatInTimeZone } from "date-fns-tz";

const DATE_STRING_FORMAT = "yyyy-MM-dd";

export function formatDate(input: Date) {
  return formatInTimeZone(input, "UTC", DATE_STRING_FORMAT);
}
