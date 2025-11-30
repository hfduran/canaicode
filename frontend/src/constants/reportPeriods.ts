export const REPORT_PERIOD_OPTIONS = [
  {
    label: "Daily - Reports sent every day at midnight UTC",
    value: "D"
  },
  {
    label: "Weekly - Reports sent every Monday at midnight UTC",
    value: "W"
  },
  {
    label: "Monthly - Reports sent on the 1st of each month at midnight UTC",
    value: "M"
  },
  {
    label: "Quarterly - Reports sent on Jan 1, Apr 1, Jul 1, Oct 1 at midnight UTC",
    value: "Q"
  },
  {
    label: "Yearly - Reports sent on January 1st each year at midnight UTC",
    value: "Y"
  }
];

export const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
