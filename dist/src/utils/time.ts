function convertTime(time: string) {
  const date = new Date(time);
  date.setHours(date.getHours() + 7);
  return date.toLocaleString("en-GB");
}

export { convertTime };
