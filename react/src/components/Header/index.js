import React from "react";
import { NavLink } from "react-router-dom";
import { makeStyles } from "@material-ui/core/styles";
import  kaartLogo  from "../../res/20-KAART-Color.svg";
import {
  AppBar,
  Toolbar,
  Typography,
  Icon,
  KaartLogo,
  KaartMenuItem,
  Link,
  GEMMenuItem,
  Button,
} from "./styles";
import "./styles.css";
const useStyles = makeStyles((theme) => ({
  button: {
    padding: "8px 8px",
  },
  selectedNavLink: {
    backgroundColor: "#4287f5",
    border: 0,
    borderRadius: 3,
    color: "White",
  },
}));
export const Header = () => {

  const classes = useStyles();

  // const kaartLogo = require("../../res/20-KAART-Color.svg");

  return (
    <AppBar>
      <Toolbar>
        <Typography>
          <Icon>
              <KaartLogo
                src={kaartLogo}
                alt="Kaart Logo"
                href="https://kaart.com/"
              />
          </Icon>
        </Typography>
        {/* This is to match kaart.com */}
        <div class="parent-div">
          <KaartMenuItem>
            <div class="dropdown">
              <div class="dropbtn">
                Services
                <i class="arrow"></i>
              </div>
              <div class="dropdown-content">
                <a href="https://kaart.com/osm/">Osm Services</a>
                <a href="https://kaart.com/gis/">Gis Consulting</a>
                <a href="https://kaart.com/dev/">Engineering</a>
              </div>
            </div>
          </KaartMenuItem>
          <KaartMenuItem>
            <div class="dropdown">
              <div href="https://kaart.com/tools/" class="dropbtn">
                Tools<i class="arrow"></i>
              </div>
              <div class="dropdown-content ">
                <a href="http://chameleon.kaart.com/">Chameleon</a>
                <a href="https://gem.kaart.com/">Gem</a>
                <a href="https://github.com/KaartGroup/GoKaart">Gokaart</a>
                <a href="https://simple.kaart.com/">Simple Gis</a>
                <a href="https://viewer.kaart.com/login">Viewer</a>
              </div>
            </div>
          </KaartMenuItem>
          <KaartMenuItem>
            <Link href="https://kaart.com/about/">About</Link>
          </KaartMenuItem>
          <KaartMenuItem>
            <Link href="https://kaart.com/careers/">Careers</Link>
          </KaartMenuItem>
        </div>
        <div class="spacer"></div>
        <GEMMenuItem>
          <NavLink to="/" className={classes.selectedNavLink}>
            <Button color="inherit" size="large">
              G E M
            </Button>
            </NavLink>
          </GEMMenuItem>
      </Toolbar>
    </AppBar>
  );
};
