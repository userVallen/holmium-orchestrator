import {
  Sidebar,
  SidebarHeader,
  SidebarContent,
  SidebarGroup,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
  SidebarFooter,
} from "@/components/ui/sidebar";
import { Button } from "@/components/ui/button";
import { SquarePen, Search, User2 } from "lucide-react";

const dummyChats = [
  {
    id: 1,
    title: "Chat #1",
  },
  {
    id: 2,
    title: "Chat #2",
  },
];

export function ChatSidebar() {
  return (
    <Sidebar>
      <SidebarHeader className="text-xl font-bold px-4 pt-4">
        Holmium
      </SidebarHeader>

      <SidebarContent className="text-black">
        <SidebarGroup>
          <SidebarMenu>
            <SidebarMenuItem>
              <Button className="text-black bg-transparent w-full justify-start hover:bg-gray-200">
                <SquarePen />
                New Chat
              </Button>
            </SidebarMenuItem>
            <SidebarMenuItem>
              <Button className="text-black bg-transparent w-full justify-start hover:bg-gray-200">
                <Search />
                Search Chats
              </Button>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarGroup>

        <SidebarGroup>
          <SidebarGroupLabel>Chats</SidebarGroupLabel>
          <SidebarMenu>
            {dummyChats.map((chat) => (
              <SidebarMenuItem key={chat.id}>
                <Button className="text-black bg-transparent w-full justify-start hover:bg-gray-200">
                  {chat.title}
                </Button>
              </SidebarMenuItem>
            ))}
          </SidebarMenu>
        </SidebarGroup>
      </SidebarContent>

      <SidebarFooter>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton>
              <User2 /> Username
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
    </Sidebar>
  );
}
