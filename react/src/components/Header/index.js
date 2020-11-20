import React from "react";
import {
  AppBar,
  Toolbar,
  ImageIcon,
  Typography,
  Icon,
  KaartLogo,
  MenuItem,
  Link,
} from "./styles";

export const Header = () => {
  const kaartLogo = require("../../res/20-KAART-Color.svg");

  return (
    <AppBar>
      <Toolbar>
          <ImageIcon>
            <Icon>
              <KaartLogo
                src={kaartLogo}
                alt="Kaart Logo"
                href="https://kaart.com/"
              />
            </Icon>
          </ImageIcon>
        <Typography></Typography>
        {/* This is to match kaart.com */}
        <MenuItem>
          <Link href="#">Services</Link>
        </MenuItem>
        <MenuItem>
          <Link href="https://kaart.com/tools/">Tools</Link>
        </MenuItem>
        <MenuItem>
          <Link href="https://kaart.com/about/">About</Link>
        </MenuItem>
        <MenuItem>
          <Link href="https://kaart.com/careers/">Careers</Link>
        </MenuItem>
        <MenuItem> <Link href="https://gem.kaart.com/">GEM</Link>
        </MenuItem>
      </Toolbar>
    </AppBar>
  );
};
