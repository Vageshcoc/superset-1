
import * as actions from '../actions/saveModalActions';
import { HYDRATE_EXPLORE } from '../actions/hydrateExplore';
export default function saveChartReducer(state = {}, action) {
    const actionHandlers = {
      //changed
      [actions.NEW_SET_SAVE_CHART_MODAL_VISIBILITY]() {
        return { ...state, isVisible: action.isVisible };
      },
      //end
      [actions.FETCH_DASHBOARDS_SUCCEEDED]() {
        return { ...state, dashboards: action.choices };
      },
      [actions.FETCH_DASHBOARDS_FAILED]() {
        return {
          ...state,
          saveModalAlert: `fetching dashboards failed for ${action.userId}`,
        };
      },
      [actions.SAVE_SLICE_FAILED]() {
        return { ...state, saveModalAlert: 'Failed to save slice' };
      },
      [actions.SAVE_SLICE_SUCCESS](data) {
        return { ...state, data };
      },
      [HYDRATE_EXPLORE]() {
        return { ...action.data.saveChartReducer };
      },
    };
  
    if (action.type in actionHandlers) {
      return actionHandlers[action.type]();
    }
    return state;
  }
  
  