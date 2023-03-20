import { ChakraProvider } from "@chakra-ui/react";

import customTheme from "../styles/theme/theme";

interface ChakraProps {
  children: React.ReactNode;
}

export const Chakra = ({ children }: ChakraProps) => {
  return <ChakraProvider theme={customTheme}>{children}</ChakraProvider>;
};
