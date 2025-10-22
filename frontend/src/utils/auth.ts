export const isAuthenticated = (): boolean => {
  const token = localStorage.getItem("token");
  const userId = localStorage.getItem("user_id");
  return !!token && !!userId;
};

export const getToken = (): string | null => {
  return localStorage.getItem("token");
};

export const getUserId = (): string | null => {
  return localStorage.getItem("user_id");
};

export const getUsername = (): string | null => {
  return localStorage.getItem("username");
};

export const logout = (): void => {
  localStorage.removeItem("token");
  localStorage.removeItem("user_id");
  localStorage.removeItem("username");
};