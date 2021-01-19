import React from "react";
import {
  makeStyles,
  createStyles,
  Theme,
  ThemeProvider,
} from "@material-ui/core/styles";
import { VotePage } from "./components/VotePage";
import { BlockchainViewer } from "./components/BlockchainViewer";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import { Appbar } from "./components/Appbar";
import { LandingPage } from "./components/LandingPage";
import { createMuiTheme } from "@material-ui/core/styles";
import { Stats } from "./components/Stats";

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    root: {
      flexGrow: 1,
    },
    paper: {
      padding: theme.spacing(2),
      textAlign: "center",
      color: theme.palette.text.secondary,
    },
  })
);

const theme = createMuiTheme({
  palette: {
    primary: {
      light: "#ffffff",
      main: "#ffffff",
      dark: "#ffffff",
      contrastText: "#ffffff",
    },
    secondary: {
      light: "#ffffff",
      main: "#ffffff",
      dark: "#ffffff",
      contrastText: "#ffffff",
    },
  },
});

export default function FullWidthGrid() {
  const classes = useStyles();

  return (
    <ThemeProvider theme={theme}>
      <div className={classes.root}>
        <Router>
          <Appbar />
          <Switch>
            <Route exact path="/">
              <LandingPage />
            </Route>
            <Route exact path="/stats">
              <Stats />
            </Route>
            <Route path="/vote/:campaign_id" component={VotePage} />
            <Route path="/blocks">
              <BlockchainViewer />
            </Route>
          </Switch>
        </Router>
      </div>
    </ThemeProvider>
  );
}
