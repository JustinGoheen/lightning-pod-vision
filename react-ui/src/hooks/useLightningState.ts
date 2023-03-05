import { useEffect, useState } from 'react';

export type LightningState = {
  vars: {
    _layout: Layout | Layout[];
    [key: string]: any;
  };
  calls: {
    [key: string]: {
      name: string;
      call_hash: string;
      ret: boolean;
    };
  };
  flows: {
    [key: string]: ChildState;
  };
  works: {
    [key: string]: any;
  };
  changes: {
    [key: string]: any;
  };
  app_state: {
    stage: AppStage;
  };
};

export type ChildState = Omit<LightningState, 'app_state'>;

export type Layout = LayoutBranch | LayoutLeaf;

export type LayoutBranch = {
  name: string;
  content: string;
};

export type LayoutLeaf = {
  name: string;
  type: LayoutType;
  source?: string;
  target: string;
};

export enum LayoutType {
  web = 'web',
  streamlit = 'streamlit',
}

export enum AppStage {
  blocking = 'blocking',
  restarting = 'restarting',
  running = 'running',
  stopping = 'stopping',
}

type WindowLightningState = {
  subscribe(handler: (state: any) => void): () => void;
  next(state: any): void;
};

declare global {
  interface Window {
    LightningState?: WindowLightningState;
  }
}

export function useLightningState() {
  const [lightningState, setLightningState] = useState<LightningState>();

  useEffect(() => {
    if (!window.LightningState) {
      return;
    }
    const unsubscribe = window.LightningState.subscribe(setLightningState);
    return unsubscribe;
  }, []);

  const updateLightningState = window.LightningState?.next;

  return { lightningState, updateLightningState };
};