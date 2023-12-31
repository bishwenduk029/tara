// src/api.ts

import axios from "axios";
import { ChatInput } from "./index";

const API_BASE_URL = "http://localhost:8000"; // Replace with your API base URL

// Create the API instance
// const api = axios.create({
//   baseURL: API_BASE_URL,
// });

const api = axios.create();

// Define the API mutation function
export const createChatMutation = async (
  chatInput: ChatInput,
  getToken: any
) => {
  const supabaseAccessToken = await getToken({
    template: "supabase-tarat-clerk",
  });
  console.log(supabaseAccessToken);
  const response = await api.post("/chats", chatInput, {
    headers: {
      Authorization: `Bearer ${supabaseAccessToken}`,
    },
  });
  return response.data;
};
