export const AuthHeader = (token: string): object => {
  return { headers: { Authorization: token } };
};

export const addDays = (date: Date, days: number): Date => {
  const result = new Date(date);
  result.setDate(date.getDate() + days);
  return result;
};
