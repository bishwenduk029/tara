import {
  Button,
  Flex,
  HStack,
  Icon,
  IconButton,
  Text,
  Tooltip,
} from "@chakra-ui/react";
import { TbRobot } from "react-icons/tb";

const Header = () => {
  return (
    <Flex width="100%" flexDirection="column" marginX="auto" px="2">
      <Flex justifyContent="space-between" py={4} as="header">
        <Flex role="group" alignItems="center" fontWeight="bold" fontSize="2xl">
          <Icon
            transition="200ms all"
            _groupHover={{ color: "brand.500" }}
            color="brand.300"
            as={TbRobot}
            mr="1"
          />
          <Text color="brand.400" display={{ base: "none", sm: "inherit" }}>
            Ava
          </Text>
        </Flex>
        <HStack spacing={1}>
          <Button size="sm" as={"a"} href="/sign-in">Login</Button>
        </HStack>
      </Flex>
    </Flex>
  );
};

export default Header;
