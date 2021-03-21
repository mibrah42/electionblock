import {
  Button,
  createStyles,
  FormControl,
  Grid,
  InputLabel,
  makeStyles,
  Select,
  Theme,
  Typography,
} from "@material-ui/core";
import React, { useState } from "react";
import landingImage from "../../assets/landingImage1.png";
import { Link } from "react-router-dom";
import { titles } from "../../data/campaigns";

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    title: {
      color: "white",
      fontWeight: "bold",
      flexWrap: "wrap",
      fontSize: "42px",
    },
    leftContent: {
      display: "flex",
      flexDirection: "column",
      marginTop: "-150px",
      maxWidth: "600px",
    },
    select: {
      borderColor: "white",
      "&:before": {
        borderColor: "white",
      },
      "&:after": {
        borderColor: "white",
      },
    },
    voteButton: {
      backgroundColor: "white",
      height: "56px",
    },
    actionItems: {
      display: "flex",
      alignItems: "center",
      justifyContent: "flex-start",
      marginTop: "16px",
    },
    bodyWrapper: {
      height: "calc(100vh - 65px)",
      width: "100vw",
      dislay: "flex",
      alignItems: "center",
      justifyContent: "center",
    },
    formControl: {
      margin: theme.spacing(1),
      minWidth: 120,
    },
    selectEmpty: {
      marginTop: theme.spacing(2),
    },
    innerWrapper: {
      display: "flex",
      alignItems: "center",
      width: "85%",
      justifyContent: "center",
    },
    link: {
      textDecoration: "none",
    },
  })
);

export function LandingPage() {
  const [campaign, setCampaign] = useState("1");

  const classes = useStyles();

  return (
    <Grid container className={classes.bodyWrapper}>
      <Grid className={classes.innerWrapper}>
        <Grid item className={classes.leftContent}>
          <Typography variant="h4" component="h1" className={classes.title}>
            An Electronic Voting System using Blockchain and Fingerprint
            Authentication
          </Typography>
          <Grid item className={classes.actionItems}>
            <FormControl variant="outlined" className={classes.formControl}>
              <InputLabel htmlFor="outlined-age-native-simple">
                Campaign
              </InputLabel>
              <Select
                color="primary"
                native
                value={campaign}
                onChange={(e) => setCampaign(e.target.value as string)}
                label="Campaign"
                inputProps={{
                  name: "campaign",
                  id: "outlined-age-native-simple",
                }}
                style={{ color: "white" }}
                className={classes.select}
              >
                <option aria-label="None" value="" />
                {titles.map((title, index) => (
                  <option value={(index + 1).toString()}>{title}</option>
                ))}
              </Select>
            </FormControl>
            <Link to={`/vote/${campaign}`} className={classes.link}>
              <Button variant="contained" className={classes.voteButton}>
                VOTE NOW
              </Button>
            </Link>
          </Grid>
        </Grid>
        <img src={landingImage} width="700px" />
      </Grid>
    </Grid>
  );
}
