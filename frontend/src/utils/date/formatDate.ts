import { format } from "date-fns";

const DATE_STRING_FORMAT = "yyyy-MM-dd"

export function formatDate(input: Date) {
    return format(input, DATE_STRING_FORMAT)
}