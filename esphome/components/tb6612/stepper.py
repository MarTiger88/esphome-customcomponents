from esphome import pins
import esphome.codegen as cg
from esphome.components import stepper
import esphome.config_validation as cv
from esphome.const import (
    CONF_ID,
    CONF_PIN_A,
    CONF_PIN_B,
    CONF_PIN_C,
    CONF_PIN_D,
    CONF_SLEEP_WHEN_DONE,
    CONF_STEP_MODE,
)

tb6612 = cg.esphome_ns.namespace("tb6612")
TB6612StepMode = tb6612.enum("TB6612StepMode")

STEP_MODES = {
    "FULL_STEP": TB6612StepMode.TB6612_STEP_MODE_FULL_STEP,
    # "HALF_STEP": TB6612StepMode.TB6612_STEP_MODE_HALF_STEP,
    # "WAVE_DRIVE": TB6612StepMode.TB6612_STEP_MODE_WAVE_DRIVE,
}

TB6612 = tb6612.class_("TB6612", stepper.Stepper, cg.Component)

CONFIG_SCHEMA = stepper.STEPPER_SCHEMA.extend(
    {
        cv.Required(CONF_ID): cv.declare_id(TB6612),
        cv.Required(CONF_PIN_A): pins.gpio_output_pin_schema,
        cv.Required(CONF_PIN_B): pins.gpio_output_pin_schema,
        cv.Required(CONF_PIN_C): pins.gpio_output_pin_schema,
        cv.Required(CONF_PIN_D): pins.gpio_output_pin_schema,
        cv.Optional(CONF_SLEEP_WHEN_DONE, default=False): cv.boolean,
        cv.Optional(CONF_STEP_MODE, default="FULL_STEP"): cv.enum(
            STEP_MODES, upper=True, space="_"
        ),
    }
).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await stepper.register_stepper(var, config)

    pin_a = await cg.gpio_pin_expression(config[CONF_PIN_A])
    cg.add(var.set_pin_a(pin_a))
    pin_b = await cg.gpio_pin_expression(config[CONF_PIN_B])
    cg.add(var.set_pin_b(pin_b))
    pin_c = await cg.gpio_pin_expression(config[CONF_PIN_C])
    cg.add(var.set_pin_c(pin_c))
    pin_d = await cg.gpio_pin_expression(config[CONF_PIN_D])
    cg.add(var.set_pin_d(pin_d))

    cg.add(var.set_sleep_when_done(config[CONF_SLEEP_WHEN_DONE]))
    cg.add(var.set_step_mode(config[CONF_STEP_MODE]))
