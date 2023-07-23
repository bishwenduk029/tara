import Hero from "./components/Hero/index.tsx";
import ChannelData from "./components/ChannelData/index.tsx";
import {
  ClerkProvider,
  SignedIn,
  SignedOut,
  SignIn,
  SignUp,
  RedirectToSignIn,
} from "@clerk/clerk-react";
import { Chakra } from "./components/Chakra.tsx";
import Header from "./layout/Header.tsx";
import { BrowserRouter, Route, Routes, useNavigate } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const queryClient = new QueryClient();

const clerkPubKey = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY;

if (!clerkPubKey) {
  throw "Missing Publishable Key";
}

const App = () => {
  return (
    <Chakra>
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <ClerkProvider publishableKey={clerkPubKey}>
            <Header />
            <Routes>
              <Route path="/" element={<Hero />} />
              <Route
                path="/sign-in/*"
                element={<SignIn routing="path" path="/sign-in" />}
              />
              <Route
                path="/sign-up/*"
                element={<SignUp routing="path" path="/sign-up" />}
              />
              <Route
                path="/chat"
                element={
                  <>
                    <SignedIn>
                      <ChannelData />
                    </SignedIn>
                    <SignedOut>
                      <RedirectToSignIn />
                    </SignedOut>
                  </>
                }
              />
            </Routes>
          </ClerkProvider>
        </BrowserRouter>
      </QueryClientProvider>
    </Chakra>
  );
};

export default App;
