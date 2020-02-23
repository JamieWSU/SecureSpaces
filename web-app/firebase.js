import app from 'firebase/app';
import * as APIKEYS from './apiKeys';
import 'firebase/database';

const config = {
  apiKey: APIKEYS.apiKey,
  authDomain: APIKEYS.authDomain,
  databaseURL: APIKEYS.databaseURL,
  projectId: APIKEYS.projectId,
  storageBucket: APIKEYS.storageBucket,
  messagingSenderId: APIKEYS.messagingSenderId,
}

class Firebase {
  constructor() {
    app.initializeApp(config);
    
    this.db = app.database();
  }

    addSyncFormToDatabase = (form) => {
      return this.db.ref('/forms/').push(form)
        .then(result => {
          let formId = result.key;
          return this.db.ref('/owners/').push({
            formId: formId
          })
        });
    }

    getSyncFormFromDatabase = formId => {
      return this.db.ref('/forms/' + formId).once('value');
    }

    /**
     * Retrieves the Sync Form associated with passed in owner ID
     */
    getSyncFormFromOwnerId = ownerId => {
      return this.db.ref('/owners/' + ownerId).once('value')
        .then((result) => {
          if (result.val() != null) {
            /* If we get a valid result, extract the correct Sync Form Id */
            const { formId } = result.val();

            /* Get the Sync Form from Firebase */
            return this.db.ref('/forms/' + formId).once('value');
          } else {
            /* TODO: Handle case where the ID is invalid for whatever reason! */
          }
        })
    }
    
    setFirebaseForm = (formId, time) => {
      return this.db.ref('/forms/' + formId + '/selectedTimes/').push({
        time
      });
    }

    getTimesForForm = formId => {
      return this.db.ref('forms/' + formId + '/times').once('value');  
    }

    getFormRef = formId => {
      return this.db.ref('/forms/' + formId + '/times/');
    }
}

const firebase = new Firebase();
export default firebase;

