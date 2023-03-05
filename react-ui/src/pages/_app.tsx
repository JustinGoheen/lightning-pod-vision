import "../styles/globals.css";
import { Container, Grid } from "@mui/material";
import NavBar from "../components/mainPage/navBar";
import { MetricsGrid } from "../components/metrics/metricsGrid";
import { SideBarGrid } from "../components/sidebar/sidebarGrid";
import { ImageGrid } from "../components/graphs/imageGrid";
import { useState } from "react";
import { useLightningState } from "../hooks/useLightningState";

const Page = () => {
  // adding state to test that React is reactive
  const [name, setName] = useState<string>();

  const { lightningState } = useLightningState();

  return (
    <>
      <NavBar />
      <br />
      <div style={{ maxWidth: "300px", margin: "0 auto" }}>
        <input value={name} onChange={event => setName(event.target.value)} />
        <div>Hello, {name || "user"}!</div>
        <h3>Lightning State:</h3>
        <div>
          <code>{JSON.stringify(lightningState, null, 2)}</code>
        </div>
      </div>
      <br />
      <Container>
        <Grid container>
          <Grid>
            <SideBarGrid />
          </Grid>
          <Grid>
            <MetricsGrid />
            <br />
            <br />
            <ImageGrid />
          </Grid>
        </Grid>
      </Container>
    </>
  );
};

export default Page;
