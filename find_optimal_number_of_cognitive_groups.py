import logging

import optuna
import pandas as pd

from mmsbm import MMSBM

from utils.utils import import_config


class Optimizer:
    def __init__(self, optuna_study, cfg):
        self.debug = cfg["optimizer"]["debug"]
        self.min_k = cfg["optimizer"]["min_user_groups"]
        self.max_k = cfg["optimizer"]["max_user_groups"]
        self.min_l = cfg["optimizer"]["min_item_groups"]
        self.max_l = cfg["optimizer"]["max_item_groups"]
        self.train = cfg["data"]["train"]
        self.test = cfg["data"]["test"]
        self.iterations = cfg["training"]["iterations"]
        self.sampling = cfg["training"]["sampling"]
        self.seed = cfg["training"]["seed"]
        self.study = optuna_study

        if self.debug:
            self.iterations = 10
            self.sampling = 2
            logger = logging.getLogger("MMSBM")
            logger.warning("Look out, you are debugging")

    def _optimize_params(self, trial):
        # Number of groups of users
        user_groups = trial.suggest_int("k", self.min_k, self.max_k)
        # Number of groups of items
        item_groups = trial.suggest_int("l", self.min_l, self.max_l)

        train = pd.read_csv("data/train_soc_5.csv")
        test = pd.read_csv("data/test_soc_5.csv")

        mmsbm = MMSBM(
            user_groups=user_groups,
            item_groups=item_groups,
            iterations=self.iterations,
            sampling=self.sampling,
            seed=1714,
            debug=self.debug,
        )
        mmsbm.cv_fit(train, folds=5)
        _ = mmsbm.predict(test)
        return mmsbm.score()["stats"]["accuracy"]

    def optimize(self, n_trials):
        try:
            self.study.optimize(self._optimize_params, n_trials=n_trials)
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(e)


if __name__ == "__main__":
    # Get parameters
    config = import_config(local=True)
    study_name = config["optimizer"]["study_name"]
    num_trials = config["optimizer"]["trials"]
    if config["optimizer"]["debug"]:
        study_name = f"{study_name}_debug"

    # Set up the study
    study = optuna.create_study(
        study_name=study_name,
        storage="sqlite:///parameters.db",
        load_if_exists=True,
        direction="maximize",
    )

    # Optimize
    optimizer = Optimizer(study, config)
    optimizer.optimize(num_trials)
