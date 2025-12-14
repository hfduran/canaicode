import { formatInTimeZone } from "date-fns-tz";

const DATE_STRING_FORMAT = "yyyy-MM-dd";
const DISPLAY_DATE_FORMAT = "dd/MM/yyyy";

export function formatDate(input: Date) {
  return formatInTimeZone(input, "UTC", DATE_STRING_FORMAT);
}

export function formatDateForDisplay(input: Date | string) {
  const date = input instanceof Date ? input : new Date(input);
  return formatInTimeZone(date, "UTC", DISPLAY_DATE_FORMAT);
}
