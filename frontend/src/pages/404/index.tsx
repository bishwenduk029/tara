// @ts-ignore
import {
  Box,
  Button,
  Heading,
  Image,
  Text,
  Link as ChakraLink,
  useColorMode,
  Flex,
} from "@chakra-ui/react";

const Page404 = () => {
  const { colorMode } = useColorMode();

  return (
    <Flex minHeight="70vh" direction="column" justifyContent="center">
      <Image src="/404 Error-pana.svg" alt="Error 404 not found Illustration" />
      <Text textAlign="center" fontSize="xs" color="gray">
        <a
          href="https://stories.freepik.com/web"
          rel="noopener noreferrer"
        >
          Illustration by Freepik Stories
        </a>
      </Text>

      <Box marginY={4}>
        <Heading textAlign="center" size="lg">
          Page not Found.
        </Heading>

        <Box textAlign="center" marginTop={4}>
          <Text fontSize="sm" color="gray">
            It&apos;s Okay!
          </Text>
          <Button
            as={"a"}
            href="/"
            backgroundColor={colorMode === "light" ? "gray.300" : "teal.500"}
            size="sm"
          >
            Let&apos;s Head Back
          </Button>
        </Box>
      </Box>
    </Flex>
  );
};

export default Page404;
