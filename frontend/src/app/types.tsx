export interface ILoadableState<T> {
  status: 'initial' | 'loaded' | 'failed'
  entity: T | null
}

export const LoadableState = {
  initial <T>(): ILoadableState<T> {
    return {
      status: 'initial',
      entity: null
    };
  },
  loaded <T>(entity: T): ILoadableState<T> {
    return {
      status: 'loaded',
      entity
    };
  },
  failed <T>(): ILoadableState<T> {
    return {
      status: 'failed',
      entity: null
    };
  }
};
