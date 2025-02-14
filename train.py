from lightning import Trainer

from dataset.hmap_dataset import HMapDataModule
from model.hmap_model import HMapLitModel
from utils import load_configs, load_pl_model, set_callbacks


def main(exp_name, pretrained_path=None, resume_path=None):
    """
    This is the main function to start training.

    Args:
        exp_name: experiment name
        pretrained_path: the path of pretrained model
        resume_path: the path of checkpoint to resume training

    Returns: None

    """

    # Load experiment configurations
    configs = load_configs(f'configs/{exp_name}.yaml')

    # Set up data module
    datamodule = HMapDataModule(**configs['data'])
    datamodule.setup()

    # Initialize model
    hmap_model = load_pl_model(HMapLitModel, pretrained_path, **configs['model'])
    hmap_model.set_predict_dataloader(datamodule.predict_dataloader)

    # Initialize trainer with callbacks
    callbacks = set_callbacks(exp_name)
    trainer = Trainer(**configs['trainer'], callbacks=callbacks)

    # Start training
    trainer.fit(hmap_model, datamodule=datamodule, ckpt_path=resume_path)


if __name__ == '__main__':
    # Start training with experiment name
    main('hmap-v4')
